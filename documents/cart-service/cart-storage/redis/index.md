# Redis store

Default production backend. Carts are protobuf bytes in `IDistributedCache`, usually StackExchange Redis. Class: `cartservice.cartstore.RedisCartStore`.

## Purpose

Store one `Cart` message per user.

## Who calls / is called by

- **Called by:** `CartService` and `HealthCheckService` when Redis (or the in-memory fallback) is selected.
- **Calls:** `IDistributedCache.GetAsync` / `SetAsync`. Redis address comes from `REDIS_ADDR`.

## Data and configuration

| Name | Role |
| --- | --- |
| `REDIS_ADDR` | Host:port (cluster default `redis-cart:6379`) |
| `CART_PERSIST_DAYS` | Cart expiration time in days (default `30`) |
| Cache key | `userId` |
| Value | `cart.ToByteArray()` / `Cart.Parser.ParseFrom` |

`EmptyCartAsync` writes an empty `Cart`.

## Architecture

`_cache` is `IDistributedCache`. Cart TTL is determined by `CART_PERSIST_DAYS` (default 30 days).

1. **Add.** Load or create cart → merge quantity by `productId` (`SingleOrDefault`) → set `ExpiresAt` → `SetAsync(userId, cart.ToByteArray())` with absolute expiration relative to now.
2. **Get.** Load bytes; parse or return `new Cart()`.
3. **Empty.** `SetAsync(userId, new Cart().ToByteArray())`.
4. **Ping.** `return true`.

Failures in add/get/empty become `RpcException(StatusCode.FailedPrecondition, $"Can't access cart storage. {ex}")`.

`src/cartservice/src/cartstore/RedisCartStore.cs`.

## Deployment

Default cluster backend is in-cluster Redis (`REDIS_ADDR=redis-cart:6379`). Helm sets `REDIS_ADDR` unless `cartDatabase.type` is `spanner`. With no backend env vars, Startup uses `AddDistributedMemoryCache` + `RedisCartStore`.

## Sources

- `src/cartservice/src/cartstore/RedisCartStore.cs`
- `src/cartservice/src/cartstore/ICartStore.cs`
- `src/cartservice/src/Startup.cs`
- `src/cartservice/src/protos/Cart.proto`
- `kubernetes-manifests/cartservice.yaml`
- `helm-chart/templates/cartservice.yaml`