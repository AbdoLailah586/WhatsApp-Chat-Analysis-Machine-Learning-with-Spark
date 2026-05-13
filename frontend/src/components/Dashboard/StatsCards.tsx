import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { MessageSquare, CheckCircle, AlertTriangle, Users } from "lucide-react"
import { motion } from "framer-motion"

interface StatsCardsProps {
  totalMessages: number
  categorizedCount: number
  urgentCount: number
  activeContacts: number
}

export function StatsCards({ totalMessages, categorizedCount, urgentCount, activeContacts }: StatsCardsProps) {
  const stats = [
    {
      title: "Total Messages",
      value: totalMessages,
      icon: MessageSquare,
      color: "text-blue-500",
    },
    {
      title: "Categorized",
      value: categorizedCount,
      icon: CheckCircle,
      color: "text-green-500",
    },
    {
      title: "Urgent",
      value: urgentCount,
      icon: AlertTriangle,
      color: "text-red-500",
    },
    {
      title: "Active Contacts",
      value: activeContacts,
      icon: Users,
      color: "text-purple-500",
    },
  ]

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat, index) => (
        <motion.div
          key={stat.title}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
        >
          <Card className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm shadow-sm hover:shadow-md transition-all">
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {stat.title}
              </CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  key={stat.value}
                >
                  {stat.value.toLocaleString()}
                </motion.span>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      ))}
    </div>
  )
}
