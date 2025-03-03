import { useState } from "react";
import InputField from "../base/input-field/InputField";
import ControlButton from "../base/nextstepbutton/ControlButton";

function CircleInput({ onDataAdded }) {
    const [radius, setRadius] = useState(null)


    const onEnterClick = () => {
        if(radius === null )
            return;
        
        const data = radius

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
                    <h2>Radius: </h2>
                </div>
                <div style={itemStyle}>
                    <InputField value=""
                        onChange={(value) => setRadius(parseInt(value))}
                        placeholder="Radius"
                        label="Radius"/>
                </div>
            </div>

            <ControlButton text={"Confirm"} onClick={onEnterClick}/>
        </div>
    )
}

export default CircleInput;