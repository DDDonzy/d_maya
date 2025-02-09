from maya.api import OpenMaya as om


class CurveData(om.MFnNurbsCurve):

    def __init__(self, controlPoints, degree):
        super().__init__()
        self.data = om.MFnNurbsCurveData().create()
        self._knots = self.generateKnots(controlPoints, degree)
        self.create(controlPoints,
                    self._knots[1:-1],
                    degree,
                    om.MFnNurbsCurve.kOpen,
                    False,
                    True,
                    self.data)

    def build(self):
        self.create(self.cvPositions(om.MFn.kWorld),
                    self.knots(),
                    self.degree,
                    self.form,
                    False,
                    True)

    def t_length(self, t=1.0):
        return self.findLengthFromParam(t)

    def parameter(self, length=0):
        return self.findParamFromLength(length)

    def get_tWeights(self, t):
        return [self.basisFunction(i, t, self.degree) for i in range(len(self.cvPositions()))]

    def generateKnots(self, controlPoints, degree):
        d = degree
        count = len(controlPoints)

        knots = [0.0] * d
        knots += [i / (count - d) for i in range(count - d + 1)]
        knots += [1.0] * d
        return knots

    def basisFunction(self, i, t, d):
        knots = self._knots
        if d == 0:
            if (knots[i] <= t < knots[i + 1]) or (t == 1 and knots[i] <= t <= knots[i + 1]):
                return 1
            else:
                return 0
        else:
            denom1 = knots[i + d] - knots[i]
            denom2 = knots[i + d + 1] - knots[i + 1]
            term1 = 0.0 if denom1 == 0.0 else (t - knots[i]) / denom1 * self.basisFunction(i,
                                                                                           t,
                                                                                           d-1)
            term2 = 0.0 if denom2 == 0.0 else (knots[i + d + 1] - t) / denom2 * self.basisFunction(i + 1,
                                                                                                   t,
                                                                                                   d-1)
            return term1 + term2
