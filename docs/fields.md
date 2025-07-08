Version: 1


| **Field Type**  | **Widgets**                            | **Note**                                                           |
| --------------- | -------------------------------------------- | ------------------------------------------------------------------ |
| `string`        | `InputText`, `InputTextarea`, `Password` | Short or long text, password input        |
| `number`        | `InputNumber`, `Slider`                      | Whole numbers, optional range with `Slider`                        |
| `float`         | `InputNumber`, `Slider`                      | Decimal input with `mode="decimal"`                                |
| `time`          | `Calendar` (`timeOnly`)                      | Time-only input (hh\:mm)                                           |
| `datetime`      | `Calendar` (`showTime`)                      | Combined date and time input                                       |
| `boolean`       | `Checkbox`, `InputSwitch`, `SelectButton`    | True/false toggle                                                  |
| `choice`        | `Dropdown`, `RadioButton`, `SelectButton`    | Select one value from a predefined list (enum-like)                |
| `multichoice`   | `MultiSelect`, `Chips`, `ListBox`            | Select multiple values from a list (many-to-many, tags, roles, etc.) |
| `foreignkey`    | `Dropdown`, `AutoComplete`, `SelectButton`   | Relation to another model (many-to-one)                            |
| `many_to_many`  | `MultiSelect`, `Chips`, `ListBox`            | Relation to multiple items (many-to-many field)                    |
| `OneToOneField` | `Dropdown`,           | Unique foreign key, can be embedded or selected                    |
| `date`          | `Calendar`                                   | Date-only selection (`yy-mm-dd`)                                   |
| `file`          | `FileUpload`                                 | Upload one or more files                                           |
| `image`         | `FileUpload` + preview (custom)              | Image file with preview                                            |
| `json`          | `CodeEditor` (custom integration)            | Monaco or Ace for editable JSON                                    |
| `color`         | `ColorPicker`                                | Color selection with HEX or RGB format                             |
