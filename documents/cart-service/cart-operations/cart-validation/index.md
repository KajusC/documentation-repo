# Cart validation

## Purpose

Validate cart input requests before items are added to the cart.

## Who calls / is called by

Called by cart services to validate incoming `AddItemRequest` payloads.

## Interfaces/Data/Configuration

- Interface: `ICartValidator`
- Class: `CartValidator`
- Method: `Task<bool> ValidateCartInput(AddItemRequest request)`
  - Returns `false` if `UserId` is null or empty, `Item.ProductId` is null or empty, or `Item.Quantity` is less than or equal to `0`.
  - Returns `true` otherwise.

## Architecture

`CartValidator` encapsulates the validation logic for cart operations to ensure data integrity.

## Deployment

Deployed as part of the cart service application.

## Sources

- `cartservice/cartstore/CartValidator.cs`
