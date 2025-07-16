import React from 'react';
import { NavLink } from 'react-router-dom';
import DashboardIcon from '@mui/icons-material/Dashboard';
import VideocamIcon from '@mui/icons-material/Videocam';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import SettingsIcon from '@mui/icons-material/Settings';
import { Box } from '@mui/material';
import './Sidebar.css';
import logo from '../assets/obscure_eye_logo.svg';

const navItems = [
  { label: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
  { label: 'Live', icon: <VideocamIcon />, path: '/live' },
  { label: 'Alerts', icon: <WarningAmberIcon />, path: '/alerts' },
  { label: 'Settings', icon: <SettingsIcon />, path: '/settings' },
];

export default function Sidebar() {
  return (
    <Box className="sidebar-root">
      <Box className="sidebar-logo-box">
        <img src={logo} alt="Obscure Eye Logo" className="sidebar-logo" />
        <div className="sidebar-title">Obscure Eye</div>
      </Box>
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              'sidebar-link' + (isActive ? ' sidebar-link-active' : '')
            }
          >
            <span className="sidebar-icon">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>
    </Box>
  );
}