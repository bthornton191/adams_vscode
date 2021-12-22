# DB_CHANGED

Returns a 1 if an element in the database has changed; returns a 0 if there was no change. 

## Format 
```java
DB_CHANGED ( ) 
```
## Argument

None 

## Example 

The following command sequence prompts you to cancel a file read, if the database contains unsaved modifications:

```java
if condition=(DB_CHANGED())
    if condition=(eval(alert("warning", "Database has changed. Continue with file read?", "Yes", "No", 2)=1))
        file bin read file=aview
    end
end
```