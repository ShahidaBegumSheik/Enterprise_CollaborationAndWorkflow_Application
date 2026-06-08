import { useEffect, useState } from "react";
import { checkoutPlan, getSubscription, verifyPayment } from "../api/billingApi";

const plans = [
  { key: "basic", name: "Basic", price: "Free", credits: 50, users: 5, storage: "100 MB",},
  { key: "silver", name: "Silver", price: "₹499", credits: 500, users: 25, storage: "1 GB", },
  { key: "gold", name: "Gold", price: "₹999", credits: 1500, users: 100, storage: "5 GB", },
];

function loadRazorpayScript() {
  return new Promise((resolve) => {
    const script = document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.onload = () => resolve(true);
    script.onerror = () => resolve(false);
    document.body.appendChild(script);
  });
}

export default function BillingPage() {
  const [subscription, setSubscription] = useState(null);
  const [error, setError] = useState("");

  async function loadSubscription() {
    const data = await getSubscription();
    setSubscription(data);
  }

  useEffect(() => {
    loadSubscription().catch(() => setError("Unable to load subscription"));
  }, []);

  async function handlePlan(plan) {
    setError("");

    try {
      const order = await checkoutPlan(plan);

      if (plan === "basic") {
        await loadSubscription();
        return;
      }

      const ok = await loadRazorpayScript();
      if (!ok) {
        setError("Unable to load Razorpay");
        return;
      }

      const options = {
        key: order.key_id,
        amount: order.amount,
        currency: order.currency,
        name: order.company_name,
        description: order.description,
        order_id: order.order_id,
        handler: async function (response) {
          await verifyPayment({
            razorpay_order_id: response.razorpay_order_id,
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_signature: response.razorpay_signature,
          });
          await loadSubscription();
        },
      };

      new window.Razorpay(options).open();
    } catch (err) {
      console.error(err);
      setError("Billing action failed");
    }
  }

  return (
    <div>
      <div className="mb-8 rounded-3xl bg-gradient-to-r from-indigo-600 to-cyan-600 p-5 text-white shadow">
        <p className="text-xs font-bold uppercase tracking-[0.35em]">SaaS Billing</p>
        <h1 className="mt-3 text-2xl lg:text-3xl font-black">Subscription & Credits</h1>
      </div>

      {error && <div className="mb-4 rounded-xl bg-red-50 p-3 text-red-700">{error}</div>}

      {subscription && (
        <div className="mb-6 rounded-2xl bg-white p-5 shadow">
          <p>Plan: <b>{subscription.plan}</b></p>
          <p>Status: <b>{subscription.status}</b></p>
          <p>Credits: <b>{subscription.credits}</b></p>
          <p>Max Users: <b>{subscription.max_users}</b></p>
          <p>Storage Limit: <b>{subscription.max_storage_mb} MB</b></p>
          <p>Amount: ₹{(subscription.amount / 100).toFixed(2)}</p>
        </div>
      )}

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {plans.map((plan) => (
          <div key={plan.key} className="rounded-2xl border bg-white p-4 shadow">
            <h2 className="text-2xl font-black">{plan.name}</h2>
            <p className="mt-3 text-3xl font-bold">{plan.price}</p>
            <p className="mt-2">{plan.credits} AI credits</p>
            <p className="mt-2">{plan.users} users</p>
            <p className="mt-2">{plan.storage} document storage</p>
            <button
              onClick={() => handlePlan(plan.key)}
              className="mt-6 rounded-xl bg-indigo-600 px-4 py-2 font-bold text-white"
            >
              Choose Plan
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

