class Descuento:
    def __init__(self):
        self.ultimo_descuento = 0  # Guarda cuánto se descontó en la última compra (opcional)

    def calcular_descuento(self, totalPagar: float) -> float:
        if totalPagar > 200000 and totalPagar <= 600000:  # 10% de descuento
            reduccion = totalPagar * 0.10
            self.ultimo_descuento = reduccion
            return totalPagar - reduccion

        elif totalPagar > 50000 and totalPagar <= 200000:  # 5% de descuento
            reduccion = totalPagar * 0.05
            self.ultimo_descuento = reduccion
            return totalPagar - reduccion

        else:  # No aplica descuento
            self.ultimo_descuento = 0
            return totalPagar

    def aplicar_descuento(self, totalPagar: float) -> float:
        return self.calcular_descuento(totalPagar)