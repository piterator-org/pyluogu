====
参考
====

.. automodule:: luogu


模型
====

.. autoclass:: luogu.Problem
   :members:

.. autoclass:: luogu.User
   :members:


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
