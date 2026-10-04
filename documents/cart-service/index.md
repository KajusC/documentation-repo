# Cart Service

ASP.NET Core gRPC service that stores a user's shopping cart and serves it back. Language: C# (`net10.0`). Package: `hipstershop.CartService`.

## Purpose

Hold cart lines (`product_id` + `quantity`) per `user_id`. Clients add items, read the cart, or empty it. The gRPC layer (`CartService`) delegates persistence to one `ICartStore` chosen at startup.

## Who calls / is called by

**Called by**

| Caller | RPCs used | How it finds cartservice |
| --- | --- | --- |
| `frontend` | `AddItem`, `GetCart`, `EmptyCart` | `CART_SERVICE_ADDR` → `cartservice:7070` |
| `checkoutservice` | `GetCart`, `EmptyCart` | `CART_SERVICE_ADDR` → `cartservice:7070` |

Kubernetes network policy and Helm authorization policy allow ingress from `frontend` and `checkoutservice` only, on port `7070`.

**Calls:** one of Redis, Cloud Spanner, or AlloyDB. Selection and config live under [Cart storage](cart-storage/index.md).

## Interfaces

Defined in `src/cartservice/src/protos/Cart.proto`:

| RPC | Request | Response |
| --- | --- | --- |
| `AddItem` | `user_id`, `CartItem` (`product_id`, `quantity`) | `Empty` |
| `GetCart` | `user_id` | `Cart` (`user_id`, `items`, `expires_at`) |
| `EmptyCart` | `user_id` | `Empty` |

Internal store contract (`ICartStore`): `AddItemAsync`, `GetCartAsync`, `EmptyCartAsync`, `Ping`. See [Cart storage](cart-storage/index.md).

gRPC health: `grpc.health.v1.Health/Check`. See [Health](health/index.md).

HTTP `GET /` returns a plaintext reminder that clients must use gRPC.

## Topics

- [Cart operations](cart-operations/index.md)
- [Cart storage](cart-storage/index.md)
- [Health](health/index.md)
- [Hosting](hosting/index.md)

## Getting started

1. Host entry is `Program.cs`: `Host.CreateDefaultBuilder` + `UseStartup<Startup>`.
2. With no backend env vars the process uses an in-memory cache behind `RedisCartStore`. See [Hosting](hosting/index.md).
3. Container listens on `7070` (`ASPNETCORE_HTTP_PORTS=7070`, `EXPOSE 7070`).
4. Tests: `src/cartservice/tests/CartServiceTests.cs` via `TestServer` + a gRPC client.

```bash
# from src/cartservice
dotnet test tests/cartservice.tests.csproj
```

Cluster deploy: `kubectl apply -f kubernetes-manifests/cartservice.yaml`.

## Architecture

```
frontend / checkoutservice
        |  gRPC :7070
        v
   CartService  (AddItem / GetCart / EmptyCart)
   HealthCheckService (Check → ICartStore.Ping)
        |
        v
   ICartStore
     ├── RedisCartStore      (protobuf bytes in IDistributedCache)
     ├── SpannerCartStore    (table CartItems)
     └── AlloyDBCartStore    (Postgres table from ALLOYDB_TABLE_NAME)
```

`CartService` does no storage of its own.

## Deployment

Image, probes, and resource limits are under [Hosting](hosting/index.md) and [Health](health/index.md). Default cluster backend is in-cluster Redis; Spanner and AlloyDB overlays are under [Cart storage](cart-storage/index.md).

## Sources

- `src/cartservice/src/protos/Cart.proto`
- `src/cartservice/src/services/CartService.cs`
- `src/cartservice/src/cartstore/ICartStore.cs`
- `src/cartservice/src/cartservice.csproj`
- `src/cartservice/src/Program.cs`
- `src/cartservice/src/Dockerfile`
- `src/cartservice/tests/CartServiceTests.cs`
- `kubernetes-manifests/cartservice.yaml`
- `src/frontend/rpc.go`
- `src/frontend/main.go`
- `src/checkoutservice/main.go`
