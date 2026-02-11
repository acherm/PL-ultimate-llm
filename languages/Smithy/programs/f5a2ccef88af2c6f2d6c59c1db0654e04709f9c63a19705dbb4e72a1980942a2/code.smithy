$version: "2.0"

namespace example.weather

/// Provides weather forecasts.
@paginated(inputToken: "nextToken", outputToken: "nextToken",
           pageSize: "pageSize")
service Weather {
    version: "2024-01-01"
    operations: [GetForecast]
}

@readonly
operation GetForecast {
    input: GetForecastInput
    output: GetForecastOutput
}

@input
structure GetForecastInput {
    @required
    city: String

    nextToken: String
    pageSize: Integer
}

@output
structure GetForecastOutput {
    forecast: Forecast
    nextToken: String
}

structure Forecast {
    @required
    temperature: Integer

    @required
    conditions: String

    humidity: Integer
}