# Add item

Feature: append a product to a user's cart, or increase quantity if that product is already present.

## Purpose

`AddItem` is how the storefront puts a SKU in the cart. The RPC validates input and forwards; each store merges quantity.

## Who calls / is called by

- **Called by:** `frontend.insertCart` → `CartService.AddItem`. Checkout does not add items.
- **Calls:** `_cartValidator.ValidateCartInput(request)`, `_cartStore.AddItemAsync(userId, productId, quantity)`.

## Interfaces

| Name | Signature |
| --- | --- |
| RPC | `AddItem(AddItemRequest) returns (Empty)` |
| Request | `user_id: string`, `item: CartItem { product_id, quantity }` |
| Store | `Task AddItemAsync(string userId, string productId, int quantity)` |
| Validator | `Task<bool> ValidateCartInput(AddItemRequest request)` |
| Errors | Throws `RpcException` (`InvalidArgument`) when validation fails; stores throw `RpcException` (`FailedPrecondition`) when storage fails |

## Architecture

`CartService.AddItem`:

1. Validate `request` via `_cartValidator.ValidateCartInput(request)`. If invalid, throw an `RpcException` with `StatusCode.InvalidArgument`.
2. Read `request.UserId`, `request.Item.ProductId`, `request.Item.Quantity`.
3. `await _cartStore.AddItemAsync(...)`.
4. Return the static `Empty` instance.

```csharp
public async override Task<Empty> AddItem(AddItemRequest request, ServerCallContext context)
{
    if (!await _cartValidator.ValidateCartInput(request))
    {
        throw new RpcException(new Status(StatusCode.InvalidArgument, "Invalid cart request"));
    }

    await _cartStore.AddItemAsync(request.UserId, request.Item.ProductId, request.Item.Quantity);
    return Empty;
}
```

`src/cartservice/src/services/CartService.cs`.

Test (`AddItem_ItemExists_Updated`): add the same product twice, expect quantity `2`, then `EmptyCart`.

## Sources

- `src/cartservice/src/protos/Cart.proto`
- `src/cartservice/src/services/CartService.cs`
- `src/cartservice/tests/CartServiceTests.cs`
- `src/frontend/rpc.go`
