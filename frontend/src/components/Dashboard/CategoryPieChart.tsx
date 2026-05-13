import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const CATEGORY_COLORS: Record<string, string> = {
  "Work": "#3B82F6",
  "Friends": "#10B981",
  "Family": "#8B5CF6",
  "Not Important": "#6B7280",
  "Promotional": "#F59E0B",
  "Spam": "#EF4444",
  "Urgent": "#DC2626",
  "Entertainment": "#EC4899"
}

interface Props {
  distribution: Record<string, number>
}

export function CategoryPieChart({ distribution }: Props) {
  const data = Object.entries(distribution).map(([name, value]) => ({
    name,
    value
  }))

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Category Distribution</CardTitle>
      </CardHeader>
      <CardContent className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={CATEGORY_COLORS[entry.name] || '#9CA3AF'} />
              ))}
            </Pie>
            <Tooltip />
            <Legend verticalAlign="bottom" height={36} />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
