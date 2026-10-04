# Cart storage

Persistence behind the gRPC handlers. One `ICartStore` is registered as a singleton at startup.

## Purpose

Keep cart lines durable (or in-process for local fallback) so `CartService` stays a thin RPC adapter.

## Who calls / is called by

- **Called by:** `CartService` (add / get / empty) and `HealthCheckService` (`Ping`).
- **Calls:** Redis cache, Spanner, or AlloyDB + Secret Manager, depending on config.

## Interfaces

```csharp
public interface ICartStore
{
    Task AddItemAsync(string userId, string productId, int quantity);
    Task EmptyCartAsync(string userId);
    Task<Hipstershop.Cart> GetCartAsync(string userId);
    bool Ping();
}
```

`src/cartservice/src/cartstore/ICartStore.cs`. Implementations: `RedisCartStore`, `SpannerCartStore`, `AlloyDBCartStore`.

## Data and configuration

Store pick in `Startup.ConfigureServices` (first match wins):

1. `REDIS_ADDR` → StackExchange Redis cache + `RedisCartStore`.
2. `SPANNER_PROJECT` or `SPANNER_CONNECTION_STRING` → `SpannerCartStore`.
3. `ALLOYDB_PRIMARY_IP` → `AlloyDBCartStore`.
4. Else in-memory distributed cache + `RedisCartStore`.

Redis carts are protobuf `Cart` blobs keyed by `userId`. Spanner table is `CartItems` (`userId`, `productId`, `quantity`). AlloyDB table name comes from `ALLOYDB_TABLE_NAME`.

## Architecture

```
ConfigureServices
    │
    ├─ REDIS_ADDR                    → RedisCartStore
    ├─ SPANNER_PROJECT / CONN STRING → SpannerCartStore
    ├─ ALLOYDB_PRIMARY_IP            → AlloyDBCartStore
    └─ (none)                        → Memory cache + RedisCartStore
```

`Ping()` on every current implementation returns `true` (the `catch` never runs). Health therefore reports `SERVING` whenever the process is up.

## Subtopics

- [Redis](redis/index.md)
- [Spanner](spanner/index.md)
- [AlloyDB](alloydb/index.md)

## Sources

- `src/cartservice/src/cartstore/ICartStore.cs`
- `src/cartservice/src/Startup.cs`
