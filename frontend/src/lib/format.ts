export function toNumber(value: string | number | undefined): number {
  return Number(value ?? 0);
}

export function formatPercent(value: number, digits = 1): string {
  return `${(value * 100).toFixed(digits)}%`;
}

export function formatDecimal(value: string | number, digits = 3): string {
  return toNumber(value).toFixed(digits);
}

export function formatCurrency(value: string | number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2,
  }).format(toNumber(value));
}
