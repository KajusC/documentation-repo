# Redis store

Default production backend. Carts are protobuf bytes in `IDistributedCache`, usually StackExchange Redis. Class: `cartservice.cartstore.RedisCartStore`.

## Purpose

Store one `Cart` message per user.

## Who calls / is called by

- **Called by:** `CartService` and `HealthCheckService` when Redis (or the in-memory fallback) is selected.
- **Calls:** `IDistributedCache.GetAsync` / `SetAsync`. Redis address comes from `REDIS_ADDR`. Cart TTL is configured via `CART_PERSIST_DAYS` (defaults to 30 days if not set or invalid).

## Data and configuration

| Name | Role |
| --- | --- |
| `REDIS_ADDR` | Host:port (cluster default `redis-cart:6379`) |
| `CART_PERSIST_DAYS` | Number of days to persist carts in cache (default `30`, manifest sets `7`) |
| Cache key | `userId` |
| Value | `cart.ToByteArray()` / `Cart.Parser.ParseFrom` |

`EmptyCartAsync` writes an empty `Cart`.

## Architecture

`_cache` is `IDistributedCache`. `CartTtl` is a static `TimeSpan` from `ReadCartTtl()`.

1. **Add.** Load or create cart → merge quantity by `productId` (`SingleOrDefault`) → set `ExpiresAt` (`expires_at` proto field to unix time seconds using `CartTtl`) → `SetAsync(userId, cart.ToByteArray(), options)` with `AbsoluteExpirationRelativeToNow` based on `CartTtl`.
2. **Get.** Load bytes; parse or return `new Cart()`.
3. **Empty.** `SetAsync(userId, new Cart().ToByteArray())` (no TTL options).
4. **Ping.** `return true`.

Failures in add/get/empty become `RpcException(StatusCode.FailedPrecondition, $"Can't access cart storage. {ex}")`.

```csharp
private static TimeSpan ReadCartTtl()
{
    var raw = Environment.GetEnvironmentVariable("CART_PERSIST_DAYS");
    if (double.TryParse(raw, out var days) && days > 0)
    {
        return TimeSpan.FromDays(days);
    }
    return TimeSpan.FromDays(30);
}
```

`src/cartservice/src/cartstore/RedisCartStore.cs`.

## Deployment

Default cluster backend is in-cluster Redis (`REDIS_ADDR=redis-cart:6379`). Kubernetes sets `CART_PERSIST_DAYS` to `7`. Helm sets `REDIS_ADDR` unless `cartDatabase.type` is `spanner`. With no backend env vars, Startup uses `AddDistributedMemoryCache` + `RedisCartStore`.

## Sources

- `src/cartservice/src/cartstore/RedisCartStore.cs`
- `src/cartservice/src/cartstore/ICartStore.cs`
- `src/cartservice/src/Startup.cs`
- `src/cartservice/src/protos/Cart.proto`
- `kubernetes-manifests/cartservice.yaml`
- `helm-chart/templates/cartservice.yaml`
