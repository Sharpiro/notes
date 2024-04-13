## Properties

- specify platform target with framework
    - `<TargetFramework>net8.0-windows</TargetFramework>`

## Force GC

```c#
// Force a garbage collection.
GC.Collect();
// Wait for all objects that are ready for finalization to be finalized.
GC.WaitForPendingFinalizers();
```

## Task Racing

```c#
public async Task Run()
{
    var my_task = GetMyTask();
    if (await Task.WhenAany(task, Task.Delay(5_000) != my_task)
    {
        throw new Exception("task timed out");
    }

    // @footgun: if you forget this you silently lose error handling!
    await my_task;
}
```

## Finally blocks

- if an error is thrown in a `catch` block, the sibling `finally` will not run

```c#
try
{
    Fail();
}
catch (Exception ex)
{
    AnotherFail();
}
finally
{
    // never gets hit because error occurred in sibling catch
}
```