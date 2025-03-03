import { useState } from "react";
import InputField from "../base/input-field/InputField";
import ControlButton from "../base/nextstepbutton/ControlButton";

function PointInput({ onDataAdded }) {
    const [x1, setX1] = useState(null)
    const [x2, setX2] = useState(null)
    const [y1, setY1] = useState(null)
    const [y2, setY2] = useState(null)


    const onEnterClick = () => {
        if(x1 === null || x2 === null || y1 === null || y2 === null)
            return;
        
        const data = {
            x1: x1,
            x2: x2,
            y1: y1,
            y2: y2
        }

        onDataAdded(data);
    }

    const containerStyle = {
        display: 'flex',
        gap: '25px',
        padding: '10px',
        backgroundColor: '#fff',
        borderRadius: '8px',
      };
    
      const itemStyle = {
        padding: '10px',
        backgroundColor: '#fff',
        border: '1px solid #ddd',
        borderRadius: '4px',
      };

    return (
        <div >
            <div style={containerStyle}>
                <div style={itemStyle}>
                    <h2>X1: </h2>
                </div>
                <div style={itemStyle}>
                    <InputField value=""
                        onChange={(value) => setX1(parseInt(value))}
                        placeholder="x1"
                        label="x1"/>
                </div>

                <div style={itemStyle}>
                    <h2>Y1: </h2>
                </div>
                <div style={itemStyle}>
                    <InputField value=""
                        onChange={(value) => setY1(parseInt(value))}
                        placeholder="y1"
                        label="y1"/>
                </div>
            </div>

            <div style={containerStyle}>
                <div style={itemStyle}>
                    <h2>X2: </h2>
                </div>
                <div style={itemStyle}>
                    <InputField value=""
                        onChange={(value) => setX2(parseInt(value))}
                        placeholder="x2"
                        label="x2"/>
                </div>

                <div style={itemStyle}>
                    <h2>Y2: </h2>
                </div>
                <div style={itemStyle}>    
                    <InputField value=""
                        onChange={(value) => setY2(parseInt(value))}
                        placeholder="y2"
                        label="y2"/>
                </div>
            </div>

            <ControlButton text={"Confirm"} onClick={onEnterClick}/>
        </div>
    )
}

export default PointInput;