import React, { useState } from 'react';
import styles from './Background.module.css';
import Dropdown from '../drop_down/DropDown';
import Brezenhem from '../../lab1/Brezenhem';
import * as cda from '../../../logic/lab1/cda';
import * as brezenhem from '../../../logic/lab1/brezentem';
import * as vu from '../../../logic/lab1/vu';
import * as circle from '../../../logic/lab2/circle';
import * as ellipse from '../../../logic/lab2/elipse';
import * as hyperbola from '../../../logic/lab2/hyperbola';
import * as parabola from '../../../logic/lab2/parabola';
import * as ermit from '../../../logic/lab3/ermit';
import * as bezier from '../../../logic/lab3/bezier';
import * as bspline from '../../../logic/lab3/b-spline';
import Circle from '../../lab2/Circle';
import Ellipse from '../../lab2/Ellipse';
import Hyperbola from '../../lab2/Hyperbola';
import Parabola from '../../lab2/Parabola';
import Ermit from '../../lab3/Ermit';
import Bezier from '../../lab3/Bezier';
import BSpline from '../../lab3/BSpline';
import Vu from '../../lab1/Vu';
import Cda from '../../lab1/CDA';
import PointInput from '../../lab1/PointInput';
import CircleInput from '../../lab2/CircleInput';
import EllipseInput from '../../lab2/EllipseInput';
import ParabolaInput from '../../lab2/ParabolaInput';
import ErmitInput from '../../lab3/ErmitInput';
import BezierInput from '../../lab3/BezierInput';
import BSplineInput from '../../lab3/BSplineInput';

function Background() {
  const [firstDropdownValue, setFirstDropdownValue] = useState(null);
  const [secondDropdownItems, setSecondDropdownItems] = useState(null);
  const [canDraw, setCanDraw] = useState(false);
  const [draw, setAlghorithm] = useState(cda.draw);
  const [name, setAlghorithmName] = useState(null);
  const [data, setData] = useState(null)

  const firstDropdownItems = ["Segments", "Second order lines", "Curves"];

  const dropdownMapping = {
    "Segments": ["CDA", "Brezenhem", "Vu"],
    "Second order lines": ["Circle", "Ellipse", "Hyperbola", "Parabola"],
    "Curves": ["Ermit", "Bezier Curve", "B-Spline"],
  };

  const alghorithmMapping = {
    "CDA": cda.draw,
    "Brezenhem": brezenhem.draw,
    "Vu": vu.draw,
    "Circle": circle.draw,
    "Ellipse": ellipse.draw,
    "Hyperbola": hyperbola.draw,
    "Parabola": parabola.draw,
    "Ermit": ermit.draw,
    "Bezier Curve": bezier.draw,
    "B-Spline": bspline.draw,
  };

  const handleFirstDropdownSelect = (itemName) => {
    setData(null)
    setFirstDropdownValue(itemName);
    setSecondDropdownItems(dropdownMapping[itemName] || []);
  };

  const handleSecondDropdownSelect = (itemName) => {
    setData(null)
    console.log("Выбрано во втором Dropdown:", itemName);
    setAlghorithmName(itemName);
    setAlghorithm(alghorithmMapping[itemName]);
    setCanDraw(true);
  };

  const onDataAdded = (data) =>
  {
    setData(data)
  }

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <div style={{ padding: "25px", textAlign: "left" }}>
          <Dropdown
            items={firstDropdownItems}
            onSelect={handleFirstDropdownSelect}
          />

          {firstDropdownValue && (
            <Dropdown
              items={secondDropdownItems}
              onSelect={handleSecondDropdownSelect}
            />
          )}
        </div>

        {canDraw && (
          <>
            {name === "CDA" && (
                <>
                    { data === null && (
                        <PointInput onDataAdded={onDataAdded}/>
                    )}

                    { data != null && (
                        <Cda
                        point1={{ x: data.x1, y: data.y1 }}
                        point2={{ x: data.x2, y: data.y2 }}
                        draw={cda.draw}
                      />
                    )
                    }
                </>
            )}
            
            {name === "Brezenhem" && (
                <>
                    { data === null && (
                        <PointInput onDataAdded={onDataAdded}/>
                    )}

                    { data != null && (
                        <Brezenhem
                        point1={{ x: data.x1, y: data.y1 }}
                        point2={{ x: data.x2, y: data.y2 }}
                        draw={brezenhem.draw}
                      />
                    )
                    }
                </>
            )}

            {name === "Vu" && (

                <>
                    { data === null && (
                        <PointInput onDataAdded={onDataAdded}/>
                    )}

                    { data != null && (
                        <Vu
                        point1={{ x: data.x1, y: data.y1 }}
                        point2={{ x: data.x2, y: data.y2 }}
                        draw={vu.draw}
                        />
                    )
                    }
                </>
            )}

            {name === "Circle" && (
                <>
                { data === null && (
                    <CircleInput onDataAdded={onDataAdded} />
                )}

                { data != null && (
                    <Circle
                    radius={data}
                    draw={circle.draw}
                    />
                )
                }
            </>                
            )}

            {name === "Ellipse" && (
                <>
                { data === null && (
                    <EllipseInput onDataAdded={onDataAdded}/>
                )}

                { data != null && (
                    <Ellipse
                a={data.a}
                b={data.b}
                draw={ellipse.draw}
                />
                )
                }
            </>           
            )} 

            {name === "Hyperbola" && (
                <>
                { data === null && (
                    <EllipseInput onDataAdded={onDataAdded}/>
                )}

                { data != null && (
                    <Hyperbola
                    a={data.a}
                    b={data.b}
                    draw={hyperbola.draw}
                    />
                )
                }
            </>
            )} 

            {name === "Parabola" && (
                <>
                { data === null && (
                    <ParabolaInput onDataAdded={onDataAdded}/>
                )}

                { data != null && (
                    <Parabola
                p={data}
                draw={parabola.draw}
                />
                )
                }
            </>
            )} 

            {name === "Ermit" && (
                <>
                { data === null && (
                    <ErmitInput onDataAdded={onDataAdded}/>
                )}

                { data != null && (
                    <Ermit
                    p= {[data.p1, data.p4]}
                    r= {[data.r1, data.r4]}
                    draw={ermit.draw}
                />
                )
                }
            </>      
            )}

            {name === "Bezier Curve" && (
                <>
                { data === null && (
                    <BezierInput onDataAdded={onDataAdded}/>
                )}

                { data != null && (
                    <Bezier
                p={[data.p1, data.p2, data.p3, data.p4]}
                draw={bezier.draw}
                />
                )
                }
            </>  
            )} 

            {name === "B-Spline" && (
                <>
                { data === null && (
                    <BSplineInput onDataAdded={onDataAdded}/>
                )}

                { data != null && (
                    <BSpline
                    p={[data.p1, data.p2, data.p3, data.p4, data.p5, data.p6, data.p7, data.p8]}
                    draw={bspline.draw}
                    />
                )
                }
            </> 
            )} 
          </>
        )}
      </div>
    </div>
  );
}

export default Background;