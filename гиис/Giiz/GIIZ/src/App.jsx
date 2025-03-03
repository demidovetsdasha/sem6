import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Background from './base/background/Background'
import ControlButton from './base/nextstepbutton/ControlButton'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>Editor</h1>
      <div>
        <Background/>
      </div>
    </>
  )
}

export default App
