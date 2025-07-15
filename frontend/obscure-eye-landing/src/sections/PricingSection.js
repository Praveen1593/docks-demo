import React from 'react';
import { Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

export default function PricingSection() {
  return (
    <Box sx={{ my: 8 }}>
      <Typography variant="h4" color="secondary" gutterBottom align="center">
        Pricing (India, 2024)
      </Typography>
      <Typography color="textSecondary" align="center" sx={{ mb: 3 }}>
        Flexible plans for every business. Custom quotes available for large deployments.
      </Typography>
      <TableContainer component={Paper} sx={{ maxWidth: 700, mx: 'auto', background: '#2d0036', border: '2px solid #a259f7' }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell style={{ color: '#cfff04', fontWeight: 'bold' }}>Tier</TableCell>
              <TableCell style={{ color: '#cfff04', fontWeight: 'bold' }}>Features</TableCell>
              <TableCell style={{ color: '#cfff04', fontWeight: 'bold' }}>Price (INR)</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>Basic</TableCell>
              <TableCell>Object detection, alerts</TableCell>
              <TableCell>₹1,500/camera/month</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Pro</TableCell>
              <TableCell>+ Emotion detection, mobile/web app</TableCell>
              <TableCell>₹3,000/camera/month</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Enterprise</TableCell>
              <TableCell>+ Custom zones, analytics, integrations</TableCell>
              <TableCell>₹5,000+/camera/month</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>On-Premises</TableCell>
              <TableCell>One-time license, 1 year support</TableCell>
              <TableCell>₹1,00,000+/site</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Custom/Enterprise</TableCell>
              <TableCell>Large deployments, custom features</TableCell>
              <TableCell>₹5,00,000+/year</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
      <Typography color="textSecondary" align="center" sx={{ mt: 2 }}>
        Contact us for a custom quote or pilot program.
      </Typography>
    </Box>
  );
}