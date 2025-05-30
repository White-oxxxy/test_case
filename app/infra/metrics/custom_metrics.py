from app.infra.metrics.prometheus_app import meter


# --- Database ---

db_query_duration = meter.create_histogram(
    name="db_query_duration_seconds",
    unit="s",
    description="Время ответа от бд"
)

db_success_counter = meter.create_counter(
    name="db_success_total",
    description="Количество успешных выполнений запросов",
)

db_error_counter = meter.create_counter(
    name="db_errors_total",
    description="Количество ошибочных выполнений запросов",
)

# --- Cache ---

cache_duration = meter.create_histogram(
    name="cache_operation_duration_seconds",
    unit="s",
    description="Время выполнения запросов в кэш"
)

cache_success_counter = meter.create_counter(
    name="task_success_total",
    description="Количество успешных выполнений кэширования",
)

cache_error_counter = meter.create_counter(
    name="task_errors_total",
    description="Количество ошибочных выполнений кэширования",
)

# --- Taskiq ---

task_duration = meter.create_histogram(
    name="task_duration_seconds",
    unit="s",
    description="Время выполнения таски",
)

task_counter = meter.create_counter(
    name="task_invocations_total",
    description="Количество вызовов таски"
)

task_success_counter = meter.create_counter(
    name="task_success_total",
    description="Количество успешных выполнений задач",
)

task_error_counter = meter.create_counter(
    name="task_errors_total",
    description="Количество ошибочных выполнений задач",
)

# --- UseCases ---

use_case_duration = meter.create_histogram(
    name="use_case_duration_seconds",
    unit="s",
    description="Время выполнения юз_кейса"
)

use_case_counter = meter.create_counter(
    name="use_case_invocations_total",
    description="Количество вызовов юз_кейса",
)

use_case_success_counter = meter.create_counter(
    name="use_case_success_total",
    description="Количество успешных выполнений кейса",
)

use_case_error_counter = meter.create_counter(
    name="use_case_errors_total",
    description="Количество ошибочных выполнений кейса",
)

# --- Controllers ---

controller_duration = meter.create_histogram(
    name="controller_duration_seconds",
    unit="s",
    description="Время выполнения контроллера"
)

controller_counter = meter.create_counter(
    name="controller_invocations_total",
    description="Количество вызовов контроллера"
)

controller_success_counter = meter.create_counter(
    name="controller_success_total",
    description="Количество успешных выполнений",
)

controller_error_counter = meter.create_counter(
    name="controller_errors_total",
    description="Количество ошибочных выполнений",
)