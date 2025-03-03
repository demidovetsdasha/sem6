import React, { useState, useRef, useEffect } from "react";
import ArrowDropDown from "./ArrowDropDown";

function Dropdown({ items, onSelect }) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [maxWidth, setMaxWidth] = useState(0);
  const buttonRef = useRef(null);

  const handleSelect = (item) => {
    setSelectedItem(item);
    setIsOpen(false);
    onSelect(item);
  };

  useEffect(() => {
    if (buttonRef.current) {
      const tempElement = document.createElement("span");
      tempElement.style.visibility = "hidden";
      tempElement.style.whiteSpace = "nowrap";
      tempElement.style.position = "absolute";
      document.body.appendChild(tempElement);

      let max = 0;
      items.forEach((item) => {
        tempElement.textContent = item;
        const width = tempElement.offsetWidth;
        if (width > max) {
          max = width;
        }
      });

      document.body.removeChild(tempElement);
      setMaxWidth(max + 64); // Добавляем отступы и место для иконки
    }
  }, [items]);

  return (
    <div style={{ position: "relative", display: "inline-block", marginRight: "10px" }}>
      {/* Кнопка для открытия/закрытия списка */}
      <button
        ref={buttonRef}
        onClick={() => setIsOpen(!isOpen)}
        style={{
          padding: "8px 16px",
          fontSize: "16px",
          cursor: "pointer",
          backgroundColor: "#DDD",
          color: "#000",
          borderRadius: "10px",
          width: `${maxWidth}px`, // Фиксированная ширина
          textAlign: "left",
          whiteSpace: "nowrap",
          display: "flex", // Используем flexbox
          alignItems: "center", // Выравниваем элементы по центру по вертикали
          justifyContent: "space-between", // Распределяем пространство между текстом и иконкой
        }}
      >
        {selectedItem || "Select"}
        <ArrowDropDown />
      </button>

      {/* Выпадающий список */}
      {isOpen && (
        <ul
          style={{
            position: "absolute",
            top: "100%",
            left: 0,
            margin: 0,
            padding: 0,
            listStyle: "none",
            border: "1px solid #ccc",
            backgroundColor: "#fff",
            zIndex: 1000,
            borderRadius: "4px",
            boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
            width: `${maxWidth}px`, // Фиксированная ширина
          }}
        >
          {items.map((item, index) => (
            <li
              key={index}
              onClick={() => handleSelect(item)}
              style={{
                padding: "8px 16px",
                cursor: "pointer",
                borderBottom: "1px solid #eee",
                color: "#000",
                whiteSpace: "nowrap",
              }}
            >
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Dropdown;