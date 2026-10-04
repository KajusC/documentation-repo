# Get cart

Feature: return the current cart for a user, including an empty cart when nothing is stored.

## Purpose

Used by the storefront to render the bag and by checkout to snapshot lines before payment.

## Who calls / is called by

- **Called by:** `frontend.getCart`; `checkoutservice.getUserCart`.
- **Calls:** `_cartStore.GetCartAsync(userId)`.

## Interfaces

| Name | Signature |
| --- | --- |
| RPC | `GetCart(GetCartRequest) returns (Cart)` |
| Request | `user_id: string` |
| Response | `Cart { user_id, repeated CartItem items }` |
| Store | `Task<Hipstershop.Cart> GetCartAsync(string userId)` |

## Architecture

`CartService.GetCart` returns the store task directly (no extra wrapping):

```csharp
public override Task<Cart> GetCart(GetCartRequest request, ServerCallContext context)
{
    return _cartStore.GetCartAsync(request.UserId);
}
```

`src/cartservice/src/services/CartService.cs`.

Test (`GetItem_NoAddItemBefore_EmptyCartReturned`): `GetCart` for a new GUID equals `new Cart()`.

## Sources

- `src/cartservice/src/protos/Cart.proto`
- `src/cartservice/src/services/CartService.cs`
- `src/cartservice/tests/CartServiceTests.cs`
- `src/frontend/rpc.go`
- `src/checkoutservice/main.go`
