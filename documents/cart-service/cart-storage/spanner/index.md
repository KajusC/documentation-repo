# Spanner store

Optional Cloud Spanner backend. Selected when Redis is unset and `SPANNER_PROJECT` or `SPANNER_CONNECTION_STRING` is set. Class: `cartservice.cartstore.SpannerCartStore`.

## Purpose

Persist cart lines as rows in table `CartItems` instead of a Redis blob.

## Who calls / is called by

- **Called by:** `CartService` / `HealthCheckService` when Spanner is selected.
- **Calls:** `Google.Cloud.Spanner.Data` (`SpannerConnection`, select / insert-or-update / DML).

## Data and configuration

| Key | Role |
| --- | --- |
| `SPANNER_CONNECTION_STRING` | If set, used as `SpannerConnectionStringBuilder.DataSource` and constructor returns |
| `SPANNER_PROJECT` | Project id when building the datasource |
| `SPANNER_INSTANCE` | Instance; default `onlineboutique` |
| `SPANNER_DATABASE` | Database; default `carts` |

Built datasource: `projects/{project}/instances/{instance}/databases/{database}`.

Table (from the Kustomize Spanner README DDL): `CartItems (userId, productId, quantity)` primary key `(userId, productId)`.

## Architecture

Constructor: a non-empty connection string wins; otherwise it builds `projects/.../instances/.../databases/...` (instance/database default to `onlineboutique` / `carts`).

- **Add.** Retriable transaction: select existing quantity for `(userId, productId)`, then insert-or-update `current + incoming`. Parameters are typed (`String`, `Int64`).
- **Get.** Select all rows for `userId`. `UserId` is assigned only when at least one row exists.
- **Empty.** `DELETE FROM CartItems WHERE userId = @userId`.
- **Ping.** `return true`.

Failures: `RpcException` / `FailedPrecondition` with `Can't access cart storage at {databaseString}`.

```csharp
if (!string.IsNullOrEmpty(spannerConnectionString)) {
    builder.DataSource = spannerConnectionString;
    databaseString = builder.ToString();
    Console.WriteLine($"Spanner connection string: ${databaseString}");
    return;
}
```

`src/cartservice/src/cartstore/SpannerCartStore.cs`.

## Deployment

Kustomize component `kustomize/components/spanner` wires the service to Spanner and removes `redis-cart`. Helm sets `SPANNER_CONNECTION_STRING` when `cartDatabase.type` is `spanner`.

## Sources

- `src/cartservice/src/cartstore/SpannerCartStore.cs`
- `src/cartservice/src/cartstore/ICartStore.cs`
- `src/cartservice/src/Startup.cs`
- `kustomize/components/spanner/README.md`
- `helm-chart/templates/cartservice.yaml`
