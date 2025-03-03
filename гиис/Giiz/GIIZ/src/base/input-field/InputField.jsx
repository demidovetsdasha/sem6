import * as React from "react";

function InputField({
  value = "",
  onChange = () => {},
  placeholder = "Введите текст",
  label = "Поле ввода"
}) {
  return (
    <div className="space-y-2">
      {label && (
        <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
          {label}
        </label>
      )}
      <input
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
};

export default InputField;