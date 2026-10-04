# Health

gRPC health used by Kubernetes probes.

## Purpose

Answer `grpc.health.v1.Health/Check` so the pod can be marked ready or alive.

## Who calls / is called by

- **Called by:** kubelet readiness and liveness probes on port `7070` (`kubernetes-manifests/cartservice.yaml`).
- **Calls:** `ICartStore.Ping()`.

## Interfaces

Mapped in `Startup.Configure`: `endpoints.MapGrpcService<cartservice.services.HealthCheckService>()`.

Class extends `Grpc.Health.V1.Health.HealthBase`. Override: `Check(HealthCheckRequest, ServerCallContext) → Task<HealthCheckResponse>`.

Status is `SERVING` when `Ping()` is true. Current stores always return `true` from `Ping()` — see [Cart storage](../cart-storage/index.md).

## Architecture

Class is `internal`. Constructor takes `ICartStore`. `request` is unused.

1. Log `Checking CartService Health`.
2. Call `Ping()`.
3. Return a completed task: `SERVING` if `Ping()` is true, else `NOT_SERVING`.

```csharp
public override Task<HealthCheckResponse> Check(HealthCheckRequest request, ServerCallContext context)
{
    Console.WriteLine("Checking CartService Health");
    return Task.FromResult(new HealthCheckResponse {
        Status = _cartStore.Ping() ? HealthCheckResponse.Types.ServingStatus.Serving
                                   : HealthCheckResponse.Types.ServingStatus.NotServing
    });
}
```

`src/cartservice/src/services/HealthCheckService.cs`.

## Deployment

```yaml
readinessProbe:
  initialDelaySeconds: 15
  grpc:
    port: 7070
livenessProbe:
  initialDelaySeconds: 15
  periodSeconds: 10
  grpc:
    port: 7070
```

Environment variables configured in deployment:
- `REDIS_ADDR`: Address of the Redis cart instance.
- `CART_PERSIST_DAYS`: Number of days to persist cart data (value set to `7`).

## Sources

- `src/cartservice/src/services/HealthCheckService.cs`
- `src/cartservice/src/cartstore/ICartStore.cs`
- `src/cartservice/src/Startup.cs`
- `kubernetes-manifests/cartservice.yaml`
