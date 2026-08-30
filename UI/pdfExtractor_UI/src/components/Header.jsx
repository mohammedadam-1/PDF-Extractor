
import "./Header.css";
import {useState} from 'react';
import {NavLink} from 'react-router-dom'

const NAV_LINKS = [
    {to: "/", lable: "Dashboard"},
    {to: "/Settings", lable: "Settings"},
]

export default function Header(){
    const [menuOpen, setMenuOpen] = useState(false)

    return (
        <header className="header-site">
            <div className="header-site__inner">
                <button
                className="header-site_toggle"
                aria-label="Toggle Layout"
                aria-expanded={menuOpen}
                onClick={() => setMenuOpen((open) => !open)}
                >
                
                </button>
                <nav className={`header-site_nav ${menuOpen ? "is-open" : ""}`}>
                    {
                        NAV_LINKS.map(({to, label}) => (
                            <NavLink
                            key={to}
                            to={to}
                            className={({isActive}) => isActive ? 'header-site_nav is-active' : ''}
                            onClick={() => setMenuOpen(false)}
                            >
                            {label}
                            </NavLink>
                        ))
                    }

                </nav>
            </div>
        </header>
    )

}