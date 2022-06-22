If you use Visual Studio Code as your code editor, your `.vscode/launch.json`
should look like this:

```json
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Demo Model",
      "type": "python",
      "request": "launch",
      "module": "very_clevr",
      "args": ["interact"],
      "justMyCode": true
    },
    {
      "name": "Train Model",
      "type": "python",
      "request": "launch",
      "module": "very_clevr",
      "args": ["train"],
      "justMyCode": true
    }
  ]
}
```
