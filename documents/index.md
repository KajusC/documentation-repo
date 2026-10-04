# Online Boutique

Cloud-first e-commerce demo. Eleven services talk over gRPC. This tree documents **cartservice** — the C# shopping-cart service.

## Table of contents

- [Cart Service](cart-service/index.md)
  - [Cart operations](cart-service/cart-operations/index.md)
    - [Add item](cart-service/cart-operations/add-item/index.md)
    - [Get cart](cart-service/cart-operations/get-cart/index.md)
    - [Empty cart](cart-service/cart-operations/empty-cart/index.md)
  - [Cart storage](cart-service/cart-storage/index.md)
    - [Redis](cart-service/cart-storage/redis/index.md)
    - [Spanner](cart-service/cart-storage/spanner/index.md)
    - [AlloyDB](cart-service/cart-storage/alloydb/index.md)
  - [Health](cart-service/health/index.md)
  - [Hosting](cart-service/hosting/index.md)

## Sources

- `microservices-demo/README.md`
- `python_env/src/main/dep.json` (extracted types, methods, calls, config, env)
