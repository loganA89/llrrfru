# Investigating Zend Framework Error on `/player/load`

## The Issue
When hitting `https://iran.fruitcraft.ir/player/load` without all expected parameters, the Zend Framework backend throws a fatal PHP error: 
`Function name must be a string in PlayerController.php line 328`

## Root Cause Analysis
In older PHP applications (like those running Zend Framework 1.x), dynamic function calls are often constructed using request parameters. For example:
```php
$storeType = $request->getPost('store_type');
$validatorFunc = "validate_" . $storeType;
$validatorFunc();
```
If `store_type` is omitted, the resulting string might be empty, or the framework might try to invoke a closure that is `null`. In PHP 7+, calling a `null` variable as a function throws exactly this fatal error: `Function name must be a string`.

## Verification in `resource.car`
Looking at `Models.Player.lua` (`loadPlayer` function), the official client explicitly attaches `store_type` based on the deployment build:
```lua
  L6_9 = _storeType
  if L6_9 then
    L6_9 = _storeType
    L5_8.store_type = L6_9
  end
```

## Verification in Legacy Scripts
Reviewing the old `exampleFr` bot scripts, the payload always explicitly included `store_type`.
* In `fruitcraft/session/session.py`: `"store_type": "persian"`
* In `Gift_card/Khabalooo(2).py`: `'store_type' : 'iraqapps'`

## The Fix
We do not need a literal `method=load` parameter because Zend uses the URL route `/player/load` to map to `PlayerController::loadAction`. The crash is caused by the server trying to dynamically execute a store validation routine without a `store_type` string.

**Resolution:** Add `"store_type": "myket"` (or `"persian"`) to the `/player/load` payload.
