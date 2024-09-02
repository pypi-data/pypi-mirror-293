The limiting hysteresis loop preisach model.
Case:
"
import preisach
B = preisach.getB(origin_H, origin_B, h)
"
origin_H is the magnetic field strength in the limiting hysteresis loop data, of type numpy array;
origin_B is the flux density data in the limiting hysteresis loop data, of type numpy array;
h is the target magnetic field strength data, of type numpy array;