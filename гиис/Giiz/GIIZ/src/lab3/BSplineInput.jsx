import { useState } from "react";
import InputField from "../base/input-field/InputField";
import ControlButton from "../base/nextstepbutton/ControlButton";

function BSplineInput({ onDataAdded }) {
    const [p1x, setP1x] = useState(null)
    const [p1y, setP1y] = useState(null)
    const [p2x, setP2x] = useState(null)
    const [p2y, setP2y] = useState(null)
    const [p3x, setP3x] = useState(null)
    const [p3y, setP3y] = useState(null)
    const [p4x, setP4x] = useState(null)
    const [p4y, setP4y] = useState(null)
    const [p5x, setP5x] = useState(null)
    const [p5y, setP5y] = useState(null)
    const [p6x, setP6x] = useState(null)
    const [p6y, setP6y] = useState(null)
    const [p7x, setP7x] = useState(null)
    const [p7y, setP7y] = useState(null)
    const [p8x, setP8x] = useState(null)
    const [p8y, setP8y] = useState(null)


    const onEnterClick = () => {
        if(p1x === null || p1y === null || p2x === null || p2y === null || p3x === null || p3y === null || p3x === null || p3y === null
            || p5x === null || p5y === null || p6x === null || p6y === null || p7x === null || p7y === null || p8x === null || p8y === null
        )
            return;
        
        const data = {
            p1: [p1x, p1y],
            p2: [p2x, p2y],
            p3: [p3x, p3y],
            p4: [p4x, p4y],
            p5: [p5x, p5y],
            p6: [p6x, p6y],
            p7: [p7x, p7y],
            p8: [p8x, p8y],
        }

        onDataAdded(data);
    }

    const containerStyle = {
        display: 'flex',
        gap: '25px',
        padding: '3px',
        backgroundColor: '#fff',
        borderRadius: '8px',
      };
    
      const itemStyle = {
        padding: '5px',
        backgroundColor: '#fff',
        border: '1px solid #ddd',
        borderRadius: '4px',
      };

    return (
        <div >
            <div style={containerStyle}>
                <div style={itemStyle}>
                    <h3>p1x: </h3>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP1x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h3>p1y: </h3>
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
                    <h3>p2x: </h3>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP2x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h3>p2y: </h3>
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
                    <h3>p3x: </h3>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP3x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h3>p3y: </h3>
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
                    <h3>p4x: </h3>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP4x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h3>p4y: </h3>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP4y(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>
            </div>

            <div style={containerStyle}>
                <div style={itemStyle}>
                    <h3>p5x: </h3>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP5x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h3>p5y: </h3>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP5y(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>
            </div>

            <div style={containerStyle}>
                <div style={itemStyle}>
                    <h3>p6x: </h3>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP6x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h3>p6y: </h3>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP6y(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>
            </div>

            <div style={containerStyle}>
                <div style={itemStyle}>
                    <h3>p7x: </h3>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP7x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h3>p7y: </h3>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP7y(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>
            </div>

            <div style={containerStyle}>
                <div style={itemStyle}>
                    <h3>p8x: </h3>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP8x(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>

                <div style={itemStyle}>
                    <h3>p8y: </h3>
                </div>
                <div style={itemStyle}>
                <InputField value=""
                        onChange={(value) => setP8y(parseInt(value))}
                        placeholder="a"
                        label="a"/>

                </div>
            </div>

            <ControlButton text={"Confirm"} onClick={onEnterClick}/>
        </div>
    )
}

export default BSplineInput;