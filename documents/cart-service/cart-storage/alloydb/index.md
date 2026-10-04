# AlloyDB store

Optional AlloyDB (Postgres) backend. Selected when Redis and Spanner keys are unset and `ALLOYDB_PRIMARY_IP` is set. Class: `cartservice.cartstore.AlloyDBCartStore`.

## Purpose

Persist cart lines in a Postgres table. Password comes from Secret Manager (`latest`).

## Who calls / is called by

- **Called by:** `CartService` / `HealthCheckService` when AlloyDB is selected.
- **Calls:** `SecretManagerServiceClient.AccessSecretVersion` at construction; `NpgsqlDataSource` for each operation.

## Data and configuration

| Key | Role |
| --- | --- |
| `PROJECT_ID` | Secret Manager project |
| `ALLOYDB_SECRET_NAME` | Secret id (`latest` version) |
| `ALLOYDB_DATABASE_NAME` | Database name |
| `ALLOYDB_PRIMARY_IP` | Host (also the Startup selector) |
| `ALLOYDB_TABLE_NAME` | Table used in SQL |

Connection string is assembled in the constructor: `Host=...;Username=postgres;Password=...;Database=...`. Username is hardcoded `postgres`.

Kustomize README defaults: database `carts`, table `cart_items`, secret `alloydb-secret`.

## Architecture

Constructor: `SecretManagerServiceClient` → `SecretVersionName(..., "latest")` → trim password → build connection string (user `postgres`) → read `ALLOYDB_TABLE_NAME`.

SQL strings interpolate `userId` / `productId` / `quantity` / `tableName` into the command text.

- **Add.** `SELECT quantity` for the pair, sum, then `INSERT ... ON CONFLICT (userId, productId) DO UPDATE SET quantity`.
- **Get.** New `Cart` with `UserId` set; `SELECT productId, quantity`; append items.
- **Empty.** `DELETE FROM {table} WHERE userID = '{userId}'`.
- **Ping.** `return true`.

Failures: `RpcException` / `FailedPrecondition` (`Unable to access cart storage due to an internal error`).

```csharp
SecretVersionName secretVersionName = new SecretVersionName(projectId, secretId, "latest");
AccessSecretVersionResponse result = client.AccessSecretVersion(secretVersionName);
string alloyDBPassword = result.Payload.Data.ToStringUtf8().TrimEnd('\r', '\n');
```

`src/cartservice/src/cartstore/AlloyDBCartStore.cs`.

## Deployment

Kustomize component `kustomize/components/alloydb`. Requires Secret Manager access and VPC reachability to the AlloyDB primary IP.

## Sources

- `src/cartservice/src/cartstore/AlloyDBCartStore.cs`
- `src/cartservice/src/cartstore/ICartStore.cs`
- `src/cartservice/src/Startup.cs`
- `kustomize/components/alloydb/README.md`
