====
安装
====

使用 pip
========

安装 PyLuogu 最简单的方式是直接在命令行执行：

.. tab:: Unix/macOS

   .. code:: shell

      python3 -m pip install --upgrade luogu

.. tab:: Windows

   .. code-block:: shell

      py -m pip install --upgrade luogu


当然，如果您希望交互式运行，可能需要安装 :mod:`PIL` 以显示验证码图片：

.. tab:: Unix/macOS

   .. code:: shell

      python3 -m pip install --upgrade 'luogu[img]'

.. tab:: Windows

   .. code-block:: shell

      py -m pip install --upgrade luogu[img]
