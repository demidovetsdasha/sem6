import { useState } from "react";
import InputField from "../base/input-field/InputField";
import ControlButton from "../base/nextstepbutton/ControlButton";

function ErmitInput({ onDataAdded }) {
    const [p1x, setP1x] = useState(null)
    const [p1y, setP1y] = useState(null)
    const [p2x, setP2x] = useState(null)
    const [p2y, setP2y] = useState(null)
    const [r1x, setR1x] = useState(null)
    const [r1y, setR1y] = useState(null)
    const [r2x, setR2x] = useState(null)
    const [r2y, setR2y] = useState(null)


    const onEnterClick = () => {
        if(p1x === null || p1y === null || p2x === null || p2y === null || r1x === null || r1y === null || r2x === null || r2y === null)
            return;
        
        const data = {
            p1: [p1x, p1y],
            p4: [p2x, p2y],
            r1: [r1x, r1y],
            r4: [r2x, r2y],
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
                    <h2>p1x: </h2>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP1x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h2>p1y: </h2>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP1y(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>
            </div>

            <div style={containerStyle}>
                <div style={itemStyle}>
                    <h2>p4x: </h2>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP2x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h2>p4y: </h2>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP2y(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>
            </div>

            <div style={containerStyle}>
                <div style={itemStyle}>
                    <h2>r1x: </h2>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setR1x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h2>r1y: </h2>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setR1y(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>
            </div>

            <div style={containerStyle}>
                <div style={itemStyle}>
                    <h2>r4x: </h2>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setR2x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h2>r4y: </h2>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setR2y(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>
            </div>

            <ControlButton text={"Confirm"} onClick={onEnterClick}/>
        </div>
    )
}

export default ErmitInput;