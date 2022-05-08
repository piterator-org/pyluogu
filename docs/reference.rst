====
参考
====

.. automodule:: luogu


模型
====

.. autoclass:: luogu.Paste
   :members:

   .. versionchanged:: 0.1
      变量 *time* 的类型自 :class:`int` 改为 :class:`datetime.datetime`

.. autoclass:: luogu.Problem

   .. autoclass:: luogu.Problem.Attachment

      .. versionchanged:: 0.1
         变量 *upload_time* 的类型自 :class:`int` 改为 :class:`datetime.datetime`

.. autoclass:: luogu.User
   :members:

   .. versionchanged:: 0.1
      变量 *register_time* 的类型自 :class:`int` 改为 :class:`datetime.datetime`


会话
====

.. autoclass:: luogu.Session
   :members:


异常
====

.. autoexception:: HttpException

.. autoexception:: AccessDeniedHttpException

.. autoexception:: luogu.NotFoundHttpException

   .. code:: json

      {
         "code": 404,
         "currentTemplate": "InternalError",
         "currentData": {
               "errorType": "LuoguFramework\\HttpFoundation\\Controller\\Exception\\HttpException\\NotFoundHttpException",
               "errorMessage": "该页面未找到",
               "errorTrace": ""
         },
         "currentTitle": "出错了",
         "currentTheme": null
      }
