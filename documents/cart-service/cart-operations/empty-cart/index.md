# Empty cart

Feature: clear every line for a user after a successful checkout or an explicit empty action.

## Purpose

`EmptyCart` removes the user's stored items. Frontend and checkout both call it.

## Who calls / is called by

- **Called by:** `frontend.emptyCart`; `checkoutservice.emptyUserCart`.
- **Calls:** `_cartStore.EmptyCartAsync(userId)`.

## Interfaces

| Name | Signature |
| --- | --- |
| RPC | `EmptyCart(EmptyCartRequest) returns (Empty)` |
| Request | `user_id: string` |
| Store | `Task EmptyCartAsync(string userId)` |

Redis keeps the key as an empty cart. Spanner and AlloyDB delete rows. See [Cart storage](../../cart-storage/index.md).

Note that the `Cart` message includes `user_id`, `items`, and `expires_at` (`int64`).

## Architecture

`CartService.EmptyCart`:

1. `await _cartStore.EmptyCartAsync(request.UserId)`.
2. Return the static `Empty` instance.

```csharp
public async override Task<Empty> EmptyCart(EmptyCartRequest request, ServerCallContext context)
{
    await _cartStore.EmptyCartAsync(request.UserId);
    return Empty;
}
```

`src/cartservice/src/services/CartService.cs`.

Tests call `EmptyCart` as cleanup after add.

## Sources

- `src/cartservice/src/protos/Cart.proto`
- `src/cartservice/src/services/CartService.cs`
- `src/cartservice/tests/CartServiceTests.cs`
- `src/frontend/rpc.go`
- `src/checkoutservice/main.go`
