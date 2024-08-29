# -*- encoding: utf-8 -*-
import abc
import traceback

from .TraceLogger import TraceLog
from .afts_client import AftsClient
from .schema import BasicAlgorithmRequest, BasicAlgorithmResponse
from .errors import *
from .StatLogger import StatLogger, TimerField, StatField, TimerUnit
from .util import *


class Context:
    traceid: str
    bizid: str
    stat: StatLogger
    afts: AftsClient
    data: dict

    def __init__(self, traceid: str):
        self._tl_ctx = TraceLog.initContext(traceid)
        self.traceid = traceid
        self.bizid = '-'
        self.data: dict = {}

    def __enter__(self):
        self._tl_ctx.begin()
        TraceLog.info(f"start context: {self}")
        dl_time = TimerField('dltime', start=False, accumulate=True, unit=TimerUnit.MS)
        up_time = TimerField('uptime', start=False, accumulate=True, unit=TimerUnit.NS)
        self.afts = AftsClient("maigc",
                               "13e049d9c34e4fd3a658b440d868204e",
                               "apwallet", dtimer=dl_time.timer, utimer=up_time.timer)
        stat_schema = (
            StatField('tid', self.traceid),
            StatField('bid'),
            StatField('errcode'),
            StatField('errmsg'),
            TimerField('tttime'),
            TimerField('pptime'),
            TimerField('extime'),
            dl_time,
            up_time,
        )
        self.stat = StatLogger("stat_session", stat_schema)
        self.stat.tttime.timer.start()
        return self

    def __exit__(self, type, value, trace):
        TraceLog.info(f"exit context: {self}")
        self.stat.tttime.timer.stop()
        self.stat.bid.set(self.bizid)
        self.stat.print()
        self._tl_ctx.end()
        return False

    def set_bizid(self, bizid: str):
        self.bizid = bizid


# 算法模块适配接口定义
class AlgorithmHandler(metaclass=abc.ABCMeta):

    # 算法模块初始化方法，服务部署时执行一次，实现环境数据准备，模型预加载，预热等逻辑
    @abc.abstractmethod
    def setup(self, work_dir, res_dir) -> bool:
        pass

    # 算法模块调用时前处理，包括数据准备、预处理和前置校验等（下载、转换、参数、数据格式校验等）
    @abc.abstractmethod
    def prepare(self, request: BasicAlgorithmRequest, context: Context):
        pass

    # 算法模块核心逻辑执行，如sd推理、模型调用等
    @abc.abstractmethod
    def execute(self, request: BasicAlgorithmRequest, context: Context) -> BasicAlgorithmResponse:
        pass

    # 算法模块上下文重置，由于handler是一个单例，reset用于在每完成一次请求处理后重置成员变量（不推荐设置成员变量）
    @abc.abstractmethod
    def reset(self, context: Context):
        pass


class Framework:

    @synchronized
    def __new__(cls, *args, **kwargs):
        if hasattr(Framework, '_instance'):
            raise ValueError('instance of <Framework> was already exist')
        Framework._instance = super().__new__(cls)
        return Framework._instance

    def __init__(self, algorithm: AlgorithmHandler, request_model: type):
        self.algorithm: AlgorithmHandler = algorithm
        self.RequestModel: type = request_model

    def setup(self, work_dir: str, res_dir: str):
        try:
            TraceLog.error(f'setup algorithm module, work-dir: {work_dir}, res-dir: {res_dir}')
            if not self.algorithm.setup(work_dir, res_dir):
                raise RuntimeError('setup algorithm env failed')
        except:
            TraceLog.error(f'setup algorithm module error: {traceback.format_exc()}')
            raise

    def process(self, features: dict, traceid: str):
        with Context(traceid) as context:
            stat = context.stat
            TraceLog.info(f"start algorithm process, request: {features}")
            # request param verify
            try:
                request:BasicAlgorithmRequest = self.RequestModel(**features)
                request.traceid = traceid
                context.set_bizid(request.bizid)
            except Exception as ex:
                errmsg = BasicErrCodes.PARAM_ERR.format(repr(ex))
                TraceLog.error(f'verify request error: {errmsg}')
                stat.errcode.set(BasicErrCodes.PARAM_ERR.value)
                stat.errmsg.set(errmsg.replace('\n', '#')[:128])
                return BasicErrCodes.PARAM_ERR.value, errmsg, None

            # algorithm executing
            try:
                TraceLog.info("reset algorithm status...")
                self.algorithm.reset(context)
                TraceLog.info("prepare algorithm executing...")
                with stat.pptime:
                    self.algorithm.prepare(request, context)
                TraceLog.info("start algorithm executing...")
                with stat.extime:
                    response = self.algorithm.execute(request, context)
                TraceLog.info(f'finish algorithm process, response: {response}')
                stat.errcode.set(response.errcode)
                stat.errmsg.set(response.errmsg)
                return (response.errcode, response.errmsg, response.data)
            except AlgorithmException as ex:
                TraceLog.error(f'algorithm execute error: {traceback.format_exc()}')
                stat.errcode.set(ex.code.value)
                stat.errmsg.set(str(ex))
                return (ex.code.value, str(ex), None)
            except Exception as ex:
                TraceLog.error(f'algorithm execute error: {traceback.format_exc()}')
                stat.errcode.set(BasicErrCodes.COMMON_ERR.value)
                stat.errmsg.set(BasicErrCodes.COMMON_ERR.format(repr(ex)))
                return (BasicErrCodes.COMMON_ERR.value, BasicErrCodes.COMMON_ERR.format(repr(ex)), None)
