## Example Usage
```python
In [1]: %load_ext inspector
In [2]: a=1; b='hello world'
In [3]: %inspect  # equivalent shortcut is %ins
             User Variables             
┏━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Name ┃ Type ┃     Size ┃ Preview     ┃
┡━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ b    │  str │ 64.0   B │ hello world │
├──────┼──────┼──────────┼─────────────┤
│ a    │  int │ 32.0   B │ 1           │
└──────┴──────┴──────────┴─────────────┘
```