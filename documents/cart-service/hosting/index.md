# Hosting

Process bootstrap: generic host, DI, store selection, and endpoint map.

## Purpose

Start an HTTP/2 Kestrel process that exposes `CartService` and `HealthCheckService` on port `7070`.

## Who calls / is called by

- **Called by:** `dotnet` / container `ENTRYPOINT ["/app/cartservice"]`.
- **Calls:** `Startup` to register stores and map gRPC endpoints.

## Data and configuration

- `appsettings.json`: `AllowedHosts=*`, Kestrel `EndpointDefaults.Protocols=Http2`.
- Docker: `ASPNETCORE_HTTP_PORTS=7070`, `DOTNET_EnableDiagnostics=0`.
- Debug Dockerfile uses `dotnet cartservice.dll` on the ASP.NET runtime image.

Store-selection env vars live under [Cart storage](../cart-storage/index.md).

## Architecture

```
Program.cs
  CreateHostBuilder → UseStartup<Startup>
        │
        ├─ ConfigureServices  (pick ICartStore, AddGrpc)
        └─ Configure          (MapGrpcService ×2, MapGet /)
```

`Startup` ctor stores `IConfiguration`. Called from `Program.CreateHostBuilder` → `UseStartup<Startup>()`. Tests use the same on `TestServer`.

**ConfigureServices** (first match):

1. `REDIS_ADDR` non-empty → `AddStackExchangeRedisCache` (`options.Configuration = redisAddress`) + `RedisCartStore`.
2. Else `SPANNER_PROJECT` or `SPANNER_CONNECTION_STRING` → `SpannerCartStore`.
3. Else `ALLOYDB_PRIMARY_IP` → log `Creating AlloyDB cart store`, `AlloyDBCartStore`.
4. Else log in-memory fallback, `AddDistributedMemoryCache` + `RedisCartStore`.
5. Always `AddGrpc()`.

**Configure:**

1. If Development → `UseDeveloperExceptionPage`.
2. `UseRouting`.
3. Endpoints: `MapGrpcService<CartService>()`, `MapGrpcService<HealthCheckService>()`, `MapGet("/", …)` writing that gRPC clients are required.

```csharp
if (!string.IsNullOrEmpty(redisAddress))
{
    services.AddStackExchangeRedisCache(options =>
    {
        options.Configuration = redisAddress;
    });
    services.AddSingleton<ICartStore, RedisCartStore>();
}
else if (!string.IsNullOrEmpty(spannerProjectId) || !string.IsNullOrEmpty(spannerConnectionString))
{
    services.AddSingleton<ICartStore, SpannerCartStore>();
}
else if (!string.IsNullOrEmpty(alloyDBConnectionString))
{
    Console.WriteLine("Creating AlloyDB cart store");
    services.AddSingleton<ICartStore, AlloyDBCartStore>();
}
else
{
    Console.WriteLine("Redis cache host(hostname+port) was not specified. Starting a cart service using in memory store");
    services.AddDistributedMemoryCache();
    services.AddSingleton<ICartStore, RedisCartStore>();
}
```

`src/cartservice/src/Startup.cs`.

```csharp
static IHostBuilder CreateHostBuilder(string[] args) =>
    Host.CreateDefaultBuilder(args)
        .ConfigureWebHostDefaults(webBuilder =>
        {
            webBuilder.UseStartup<Startup>();
        });
```

`src/cartservice/src/Program.cs`.

## Deployment

- Image built from `src/cartservice/src/Dockerfile`: SDK publish (single-file, trimmed) onto `dotnet/runtime-deps` chiseled, user `1000`.
- Kubernetes `Deployment` + `Service` (`ClusterIP`, port `7070`) + `ServiceAccount` in `kubernetes-manifests/cartservice.yaml`.
- Environment variables in deployment include `REDIS_ADDR` and `CART_PERSIST_DAYS` (set to `7`).
- Requests `200m` CPU / `64Mi`; limits `300m` / `128Mi`.
- Default cluster backend is in-cluster Redis; see [Redis store](../cart-storage/redis/index.md).

## Sources

- `src/cartservice/src/Program.cs`
- `src/cartservice/src/Startup.cs`
- `src/cartservice/src/appsettings.json`
- `src/cartservice/src/Dockerfile`
- `src/cartservice/tests/CartServiceTests.cs`
- `kubernetes-manifests/cartservice.yaml`
