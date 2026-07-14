from pydantic import BaseModel


class TrainingResponse(BaseModel):
    status: str
    model_version: str
    training_metrics: dict[str, float | int | str]
    validation_messages: list[str]
    training_plot_url: str | None = None
    evaluation_metrics: dict[str, float | int | str]
    actual_vs_predicted_plot_url: str | None = None
    residual_plot_path_url: str | None = None
