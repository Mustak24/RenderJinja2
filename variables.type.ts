type TaxSummary = {
  entity: string;
  taxable_value: number;
  igst: number;
  cgst: number;
  sgst: number;
  tax_amount: number;
};

type Totals = {
  taxable_value: number;
  igst: number;
  cgst: number;
  sgst: number;
  tax_amount: number;
};

type InvoiceItem = {
  item_id: string;
  name: string;
  pack: string;
  hsn: string;
  qty: number;
  rate: number;
  amount: number;
  discount_amount: number;
  tax_rate: string;
  tax_amount: number;
  total_amount: number;
};

type Invoice = {
  voucher_type: string;
  voucher_number: string;
  date: string;
  vehicle_number: string;
  mode_of_transport: string;
  payment_mode: string;
  place_of_supply: string;

  total: number;
  discount: number;
  total_amount: number;
  total_tax: number;
  additional_charge: number;
  roundoff: number;
  grand_total: number;

  is_reversed_charge: string;

  tax_code: string;
  totals: Totals;

  tax_headers: string[];
  taxes: TaxSummary[];

  items: InvoiceItem[];
};

type Party = {
  name: string;
  mailing_address: string;
  mailing_state: string;
  mailing_country: string;
  mailing_pincode: string;

  phone: string;
  email: string;
  tin: string;

  bank_name: string;
  bank_branch: string;
  account_no: string;
  account_name: string;
  ifsc: string;
};

type Phone = {
  code: string;
  number: string;
};

type Company = {
  company_name: string;
  address_1: string;
  address_2: string;
  state: string;
  country: string;
  pinCode: string;

  phone: Phone;
  email: string;
  tin: string;

  bank_name: string;
  bank_branch: string;
  account_no: string;
  account_name: string;
  ifsc: string;

  qr_code_url: string;
  motto: string;
};

type TemplateVars = {
  invoice: Invoice;
  party: Party;
  company: Company;
};