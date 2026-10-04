# Cart validation

## Purpose

Validates cart input requests to ensure that the user ID, product ID, and item quantity are valid before adding items to the cart.

## Who calls / is called by

Called by the cart service operations to validate incoming `AddItemRequest` payloads.

## Interfaces/Data/Configuration

Implements `ICartValidator` with the `ValidateCartInput(AddItemRequest request)` method. Validates that:
- `request.UserId` is not null or empty.
- `request.Item.ProductId` is not null or empty.
- `request.Item.Quantity` is greater than 0.

## Architecture

The `CartValidator` class evaluates the request fields sequentially and returns a boolean task indicating whether the input is valid.

## Sources

- cartservice/cartstore/CartValidator.cs
