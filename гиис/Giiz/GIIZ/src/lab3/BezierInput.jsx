import { useState } from "react";
import InputField from "../base/input-field/InputField";
import ControlButton from "../base/nextstepbutton/ControlButton";

function BezierInput({ onDataAdded }) {
    const [p1x, setP1x] = useState(null)
    const [p1y, setP1y] = useState(null)
    const [p2x, setP2x] = useState(null)
    const [p2y, setP2y] = useState(null)
    const [p3x, setP3x] = useState(null)
    const [p3y, setP3y] = useState(null)
    const [p4x, setP4x] = useState(null)
    const [p4y, setP4y] = useState(null)


    const onEnterClick = () => {
        if(p1x === null || p1y === null || p2x === null || p2y === null || p3x === null || p3y === null || p3x === null || p3y === null)
            return;
        
        const data = {
            p1: [p1x, p1y],
            p2: [p2x, p2y],
            p3: [p3x, p3y],
            p4: [p4x, p4y],
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
                    <h2>p2x: </h2>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP2x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h2>p2y: </h2>
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
                    <h2>p3x: </h2>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP3x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h2>p3y: </h2>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP3y(parseInt(value))}
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
                        onChange={(value) => setP4x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h2>p4y: </h2>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP4y(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>
            </div>

            <ControlButton text={"Confirm"} onClick={onEnterClick}/>
        </div>
    )
}

export default BezierInput;