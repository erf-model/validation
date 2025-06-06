# Flow Over Terrain

Details regarding the Witch of Agnesi (WOA) test case may be found in [Sridhar et al. (2022)](https://doi.org/10.5194/gmd-15-6259-2022).
    
Results presented herein were generated with ERF hash: **9428c70** and inputs file: [inputs](https://github.com/erf-model/ERF/tree/development/Exec/DryRegTests/WitchOfAgnesi/inputs).
     
Specification of the terrain height at the bottom of the domain follows $z(x) = \frac{h_{m} a^2}{\left( x - x_c\right)^2 + a^2}$, where $h_m$ = 1[m] and $a = 1000$ [m]. The domain lengths are $(L_x, L_z) = (144\times 10^3, 20\times 10^3)$ [m] and the  horizontal direction has a uniform grid resolution of $\Delta x = 500$ [m]. The mesh is geometrically stretched in the vertical to provide improved resolution near the hill; an initial spacing of 0.1 [m] and a stretching ratio of 1.05 is utilized in the vertical direction. The simulation is run for 3 hours, with an RK3 time step of 0.03 [s] and 4 acoustic sub-steps in the last RK stage. Inflow-outflow boundary conditions were applied in the stream-wise direction, with a 10 [m/s] inflow velocity, and slip walls were utilized at the top and bottom. The $3^{\rm rd}$ order upwind scheme was used for advection. This test case is purely inviscid and dry.

<div style="display: flex;">
  <img src="WoA_mesh.png" alt="Vertically stretched mesh" width="40%" height="40%" style="margin-right: 10px;"> <img src="WoA_zvel.png" alt="Vertical velocity profile" width="50%" height="50%">
</div>

*Vertically stretched mesh and vertical velocity profile for the Witch of Agnesi (WOA) hill.*

## Analytical solution

The `ExactSolution` directory has the routine to compute the analytical solution for this test case. See sections 3.7 and 6.7 in [Giraldo and Restelli (2008)](https://www.sciencedirect.com/science/article/abs/pii/S0021999107005384). The analytical solution is computed following [Smith (1979)](https://www.tandfonline.com/doi/pdf/10.3402/tellusa.v32i4.10590). The figure below shows the comparison with Fig. 12(b) of [Giraldo and Restelli (2008)](https://www.sciencedirect.com/science/article/abs/pii/S0021999107005384). The routine can be compiled and run as 
```
mpicxx -std=c+++14 main.cpp -o WoA.exe
./WoA.exe
```
This writes out the vertical velocity contours into a `vtk` file - `WoA_zvel.vtk` that can be read in VisIt or ParaView.

**UPDATE**: An alternative python script (`WOA_1D_FFT.py`) has been provided with improved agreement with Giraldo and Restelli.

