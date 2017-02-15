require 'spec_helper'
describe '${module_name}' do

  context 'for all systems' do
    let(:facts) {{ :operatingsystemmajrelease => '7', :osfamily => 'Redhat' }}

    context 'with defaults for all parameters' do
      it { should contain_class('${module_name}') }
    end

  end

end


