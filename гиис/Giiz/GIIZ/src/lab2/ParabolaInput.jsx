import { useState } from "react";
import InputField from "../base/input-field/InputField";
import ControlButton from "../base/nextstepbutton/ControlButton";

function ParabolaInput({ onDataAdded }) {
    const [a, setA] = useState(null)


    const onEnterClick = () => {
        if(a === null)
            return;
        
        const data = a

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
                    <h2>p: </h2>
                </div>
                <div style={itemStyle}>
                    <InputField value=""
                        onChange={(value) => setA(parseInt(value))}
                        placeholder="a"
                        label="a"/>
                </div>
            </div>

            <ControlButton text={"Confirm"} onClick={onEnterClick}/>
        </div>
    )
}

export default ParabolaInput;