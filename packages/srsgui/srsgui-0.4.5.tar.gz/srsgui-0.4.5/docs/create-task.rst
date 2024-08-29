
Writing a task script
-----------------------

When you write a Python script that runs with ``srsgui``, you make a subclass of
:class:`Task <srsgui.task.task.Task>` class, and implement
:meth:`setup<srsgui.task.task.Task.setup>`,
:meth:`test<srsgui.task.task.Task.test>` and
:meth:`cleanup<srsgui.task.task.Task.cleanup>`.

Following is the simplest form of a task. Even though it does not do much,
``srsgui`` is happy to run the task, if it is included in a .taskconfig file.

.. _top-of-bare-bone-task:

.. code-block::

    from srsgui import Task

    class ZerothTask(Task):
        def setup(self):
            print('Setup done.')

        def test(self):
            print('Test finished.')

        def cleanup(self):
            print('Cleanup done.')

When a task runs, the setup() method runs first. if the setup finished with an exception,
the task is aborted without running test() or cleanup(). If the setup() method completes
without exception, the test() method runs next. Regardless of any exceptions,
the cleanup() method runs last.

Your task may be much more involved of course, utilizing the resources and APIs
provided in the Task class for Graphical User Interface (GUI) inputs and outputs. 
As long as your tasks make proper use of the GUI resources available from the :class:`Task <srsgui.task.task.Task>` class,
your task will run successfully in the ``srsgui`` application.

A task is executed as a Python thread_ (if it is run by an application with a Qt backend,
it will be QThread_.), running concurrently with the main application.

The :class:`Task <srsgui.task.task.Task>` is designed with much consideration
on protection of the main application from crashing caused by unhandled Exceptions. 
``srsgui`` provides debug information and error handling just as Python interpreter does. 

If you have modified a task, reopen the .taskconfig file from within ``srsgui`` in order to reload
the modified task before you run it again (otherwise your modified code will not be run).


The main application provides resources that a task can use,
and responds to the callbacks from the task. The resources are set using
the APIs provided by the task.

    - :meth:`set_inst_dict <srsgui.task.task.Task.set_inst_dict>` -- 
      set the instrument dictionary that contains the instrument instances.
    - :meth:`set_data_dict <srsgui.task.task.Task.set_data_dict>` -- 
      set the data dictionary that contains the data instances.
    - :meth:`set_figure_dict <srsgui.task.task.Task.set_figure_dict>` -- 
      set the figure dictionary that contains the figure instances.
    - :meth:`set_session_handler <srsgui.task.task.Task.set_session_handler>` -- 
      set the session handler that saves the data to a file.
    - :meth:`set_callback_handler <srsgui.task.task.Task.set_session_handler>` -- 
      set the callback handler that handles the callbacks from the task.


The main application and the running task are separate threads, and the main application responds only to
the callbacks from the task. Following are convenience methods for callbacks and related ones
in the :class:`Task <srsgui.task.task.Task>` class.

For text output,
    - :meth:`write_text <srsgui.task.task.Task.write_text>` is the base method for Task to use
      :meth:`callbacks.text_available <srsgui.task.callbacks.Callbacks.text_available>` callback.
    - :meth:`display_device_info <srsgui.task.task.Task.display_device_info>`
    - :meth:`display_result <srsgui.task.task.Task.display_result>`
    - :meth:`update_status <srsgui.task.task.Task.update_status>`
    - :meth:`print <srsgui.ui.taskmain.TaskMain.print_redirect>`

For python logging_,
    - :meth:`get_logger <srsgui.task.task.Task.get_logger>` is to get the logger instance for the task.
    - ``logger.debug`` is to use the logger instance to log debug messages.
    - ``logger.info`` is to use the logger instance to log info messages.
    - ``logger.error`` is to use the logger instance to log error messages.
    - ``logger.warning`` is to use the logger instance to log warning messages.
    - ``logger.critical`` is to use the logger instance to log critical messages.


For the input panel in the ``srsgui`` main window,
    :attr:`input_parameters <srsgui.task.task.Task.input_parameters>` is a dictionary that contains
    the input parameters that will be displayed in the input panel.

    - :meth:`get_all_input_parameters <srsgui.task.task.Task.get_all_input_parameters>` is to get all the input
      parameters that are displayed in the input panel.
    - :meth:`set_input_parameter <srsgui.task.task.Task.set_input_parameter>` is to set the value of an input
      parameter.
    - :meth:`get_input_parameter <srsgui.task.task.Task.get_input_parameter>` is to get the value of an input
      parameter.
    - :meth:`notify_parameter_changed <srsgui.task.task.Task.notify_parameter_changed>` is to notify the
      main application that the value of an input parameter has changed. The main application will
      update the value of the input parameter in the input panel.

For Matplotlib `figures <figure_>`_,
    You can use most of Axes_-based Matplotlib APIs with the figure instance you get with
    :meth:`get_figure <srsgui.task.task.Task.get_figure>`. After adding data and formats
    into the figure, call :meth:`request_figure_update <srsgui.task.task.Task.request_figure_update>`.

    - :meth:`get_figure <srsgui.task.task.Task.get_figure>`
    - :meth:`request_figure_update <srsgui.task.task.Task.request_figure_update>`
    - :meth:`notify_data_available <srsgui.task.task.Task.notify_data_available>`
    - :meth:`clear_figures <srsgui.task.task.Task.clear_figures>`

For a question dialog box during running a task,
    - :meth:`ask_question <srsgui.task.task.Task.ask_question>`
    - :meth:`question_background_update <srsgui.task.task.Task.question_background_update>`

For the session_handler (which saves information from a task to a file),
    - :meth:`add_details <srsgui.task.task.Task.add_details>`
    - :meth:`create_table <srsgui.task.task.Task.create_table>`
    - :meth:`add_data_to_table <srsgui.task.task.Task.add_data_to_table>`
    - :meth:`create_table_in_file <srsgui.task.task.Task.create_table_in_file>`
    - :meth:`add_to_table_in_file <srsgui.task.task.Task.add_to_table_in_file>`

For inst_dict
    - :meth:`get_instrument <srsgui.task.task.Task.get_instrument>` is to retrieve
      the Instrument subclass instance named in the \.taskconfig file. Once getting
      the instrument instance, you can use it in the task in the same way with
      the instance created from a Python interpreter.

Once you get used to the API for the :class:`Task <srsgui.task.task.Task>` class,
you can write scripts that run as a part of ``srsgui``.


.. _PyVisa: https://pyvisa.readthedocs.io/en/latest/
.. _srsinst.sr860: https://pypi.org/project/srsinst.sr860/
.. _VXI11: https://www.lxistandard.org/About/VXI-11-and-LXI.aspx
.. _GPIB: https://en.wikipedia.org/wiki/IEEE-488
.. _USB-TMC: https://www.testandmeasurementtips.com/remote-communication-with-usbtmc-faq/
.. _thread: https://docs.python.org/3/library/threading.html
.. _QThread: https://doc.qt.io/qt-6/qthread.html
.. _logging: https://docs.python.org/3/howto/logging.html
.. _figure: https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure
.. _axes: https://matplotlib.org/stable/api/axes_api.html