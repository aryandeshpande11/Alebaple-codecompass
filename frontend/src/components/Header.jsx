import {
  Header as CarbonHeader,
  HeaderName,
  HeaderGlobalBar,
  HeaderGlobalAction,
  SkipToContent
} from '@carbon/react'
import { Asleep, Light, Ai } from '@carbon/icons-react'

function Header({ theme, setTheme }) {
  const toggleTheme = () => {
    setTheme(theme === 'white' ? 'g10' : 'white')
  }

  return (
    <CarbonHeader aria-label="Code Onboarding Accelerator">
      <SkipToContent />
      <HeaderName href="/" prefix="IBM">
        <Ai size={20} style={{ marginRight: '0.5rem' }} />
        Code Onboarding Accelerator
      </HeaderName>
      <HeaderGlobalBar>
        <HeaderGlobalAction
          aria-label="Toggle theme"
          onClick={toggleTheme}
          tooltipAlignment="end"
        >
          {theme === 'white' ? <Asleep size={20} /> : <Light size={20} />}
        </HeaderGlobalAction>
      </HeaderGlobalBar>
    </CarbonHeader>
  )
}

export default Header

// Made with Bob - Enterprise Edition
