import React from 'react';
import styles from './ControlButton.module.css';

function ControlButton({text, onClick}) {
  return (
    <div style={{ display: "inline-block", marginRight: "150px"}}>
        <button className={styles.button} onClick={onClick}>
      <span className={styles.text}>{text}</span>
      <img
        src="https://cdn.builder.io/api/v1/image/assets/TEMP/e299191eedaa63daea67b1d47179dd7b2ef008b81acc89715bff9456a1ac69c4?placeholderIfAbsent=true&apiKey=d25c8be4e1ba474db85eadc219f144b3"
        alt=""
        className={styles.icon}
      />
    </button>
    </div>
  );
};

export default ControlButton;