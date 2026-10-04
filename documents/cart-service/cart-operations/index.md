# Cart operations

The public gRPC surface of cartservice. Three RPCs on `hipstershop.CartService` cover the whole cart lifecycle.

## Purpose

Let shoppers accumulate lines, let the storefront render the cart, and let checkout read then clear it.

## Who calls / is called by

- **Called by:** `frontend` (`AddItem`, `GetCart`, `EmptyCart`); `checkoutservice` (`GetCart`, `EmptyCart`).
- **Calls:** `ICartStore` (`AddItemAsync`, `GetCartAsync`, `EmptyCartAsync`).

## Interfaces

```protobuf
service CartService {
    rpc AddItem(AddItemRequest) returns (Empty) {}
    rpc GetCart(GetCartRequest) returns (Cart) {}
    rpc EmptyCart(EmptyCartRequest) returns (Empty) {}
}
```

Handlers live in `cartservice.services.CartService`, which extends `Hipstershop.CartService.CartServiceBase`. Mapped in `Startup.Configure` via `endpoints.MapGrpcService<CartService>()`.

## Architecture

Each RPC is a thin pass-through:

1. Read fields off the protobuf request.
2. Await the matching `ICartStore` method.
3. Return `Empty` (add / empty) or `Cart` (get).

Storage-specific merge and SQL behavior is documented under [Cart storage](../cart-storage/index.md).

## Subtopics

- [Add item](add-item/index.md)
- [Get cart](get-cart/index.md)
- [Empty cart](empty-cart/index.md)

## Sources

- `src/cartservice/src/protos/Cart.proto`
- `src/cartservice/src/services/CartService.cs`
- `src/cartservice/src/Startup.cs`
