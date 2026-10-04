# Cart Validation

## Purpose

Validates cart input data to ensure user IDs, product IDs, and quantities are correctly specified before adding items to the cart.

## Who calls / is called by

Called by cart operation handlers to validate incoming `AddItemRequest` payloads.

## Interfaces/Data/Configuration

- `ICartValidator`: Interface defining `Task<bool> ValidateCartInput(AddItemRequest request)`.
- `CartValidator`: Implementation that returns false if `UserId` is null or empty, `Item.ProductId` is null or empty, or `Item.Quantity` is less than or equal to zero. Returns true otherwise.

## Architecture

Encapsulated in the `cartservice.cartstore` namespace as a modular validation component.

## Deployment

Part of the cart service deployment.

## Sources

- cartservice/cartstore/CartValidator.cs