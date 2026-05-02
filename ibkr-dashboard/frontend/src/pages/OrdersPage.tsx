import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs'
import { OpenOrdersTable } from '../components/orders/OpenOrdersTable'
import { FilledOrdersTable } from '../components/orders/FilledOrdersTable'

export function OrdersPage() {
  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-semibold">Orders</h1>
      <Tabs defaultValue="open">
        <TabsList>
          <TabsTrigger value="open">Open</TabsTrigger>
          <TabsTrigger value="filled">Filled</TabsTrigger>
          <TabsTrigger value="cancelled">Cancelled</TabsTrigger>
        </TabsList>
        <TabsContent value="open">
          <OpenOrdersTable />
        </TabsContent>
        <TabsContent value="filled">
          <FilledOrdersTable status="filled" />
        </TabsContent>
        <TabsContent value="cancelled">
          <FilledOrdersTable status="cancelled" />
        </TabsContent>
      </Tabs>
    </div>
  )
}
